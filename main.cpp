#include <QCoreApplication>
#include <opencv2/core.hpp>

#define FINAL_LEVEL 5

using namespace cv;

vector<> beamCurve;
<> constructBeamCurve(int level, <> prevBeamCurve);
void initializeBeamCurve(&<>);
... stitchTiles(..., int hTile, int vTile);
void processTile(tile);

double response(Mat& tile, Point p1, Point p2);
double meanIntensityStLine(Mat& tile, Point p1, Point p2);
double integrate(Mat& tile, Point p1, Point p2);
double L(Mat& tile, Point p1, Point p2);
int onOppositeSide(Mat &tile, Point p1, Point p2, int& side);
double parallelogramResp(Mat &tile, Point p1, Point p2, int side);
double quadrilateralResp(Mat &tile, Point p1, Point p2, int& side);
void computeTileResp(tile);

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    return a.exec();
}

double response() {
    initializeBeamCurve(beamCurve[0]);
    for (int level=3; level<FINAL_LEVEL; level++) {
        beamCurve[level-2] = constructBeamCurve(level, beamCurve[level-1-2]);
    }
    processTile(beamCurve[FINAL_LEVEL]);
}

void initializeBeamCurve(&<>) {
    for (int col=0; col<...; col+=5) {
        for (int row=0; row<...; row+=5) {
            tile = getTile(..., col, row);
            computeTileResp(tile);
        }
    }
}

<> constructBeamCurve(int level, <> prevBeamCurve) {
    for (int hTile=0; hTile<...; hTile+=2) {
        for (int vTile=0; vTile<...; vTile+=2) {
            tile = stitchTiles(..., hTile, vTile);
        }
    }
}

... stitchTiles(..., int hTile, int vTile) {
    // Stitch and retain curve with resp > threshold

}

void processTile(tile) {
    dropWeakCurves(tile);
    dropScaterredCurves(tile);
    applySpatialNonMaxSuppression(tile);
    applyInterLevelSuppression(tile);
}

void computeTileResp(tile) {
    for (int i=0; i<5; i++) {
        for (int j=0; j<5; j++) {
            tileResponse(tile, PointI, PointJ);
    }
}

double tileResponse(Mat& tile, Point p1, Point p2) {
    int side;

    if (onOppositeSide(tile, p1, p2, side) != 0) {
        return parallelogramResp(tile, p1, p2, side);
    }
    else {
        return quadrilateralResp(tile, p1, p2, side);
    }
}

int onOppositeSide(Mat &tile, Point p1, Point p2, int& side) {
    side = 1;
    return 1;
}

double parallelogramResp(Mat &tile, Point p1, Point p2, int side) {
    double sum1=0, sum2=0;

    if (side == 0) {
        for (int s=1; s=tile.cols/2; s++) {
            sum1 += (L(tile, Point(p1.x+s, p1.y), Point(p2.x+s, p2.y)) *
                        meanIntensityStLine(tile, Point(p1.x+s, p1.y), Point(p2.x+s, p2.y))) -
                    (L(tile, Point(p1.x-s, p1.y), Point(p2.x-s, p2.y)) *
                        meanIntensityStLine(tile, Point(p1.x-s, p1.y), Point(p2.x-s, p2.y)));
            sum2 += L(tile, Point(p1.x+s, p1.y), Point(p2.x+s, p2.y)) -
                    L(tile, Point(p1.x-s, p1.y), Point(p2.x-s, p2.y));
        }
    }
    else {
        for (int s=1; s=tile.cols/2; s++) {
            sum1 += (L(tile, Point(p1.x, p1.y+s), Point(p2.x, p2.y+s)) *
                        meanIntensityStLine(tile, Point(p1.x, p1.y+s), Point(p2.x, p2.y+s))) -
                    (L(tile, Point(p1.x, p1.y-s), Point(p2.x, p2.y-s)) *
                        meanIntensityStLine(tile, Point(p1.x, p1.y-s), Point(p2.x, p2.y-s)));
            sum2 += L(tile, Point(p1.x, p1.y+s), Point(p2.x, p2.y+s)) -
                    L(tile, Point(p1.x, p1.y-s), Point(p2.x, p2.y-s));
        }
    }
    return fabs(sum1/sum2);
}

double quadrilateralResp(Mat &tile, Point p1, Point p2, int& side) {
    double sum1=0, sum2=0;

    if (side == 0) {
        for (int s=1; s=tile.cols/2; s++) {
            sum1 += (L(tile, Point(p1.x+s, p1.y), Point(p2.x, p2.y+s)) *
                        meanIntensityStLine(tile, Point(p1.x+s, p1.y), Point(p2.x, p2.y+s))) -
                    (L(tile, Point(p1.x-s, p1.y), Point(p2.x, p2.y-s)) *
                        meanIntensityStLine(tile, Point(p1.x-s, p1.y), Point(p2.x, p2.y-s)));
            sum2 += L(tile, Point(p1.x+s, p1.y), Point(p2.x, p2.y+s)) -
                    L(tile, Point(p1.x-s, p1.y), Point(p2.x, p2.y-s));
        }
    }
    else {
        for (int s=1; s=tile.cols/2; s++) {
            sum1 += (L(tile, Point(p1.x, p1.y+s), Point(p2.x+s, p2.y)) *
                        meanIntensityStLine(tile, Point(p1.x, p1.y+s), Point(p2.x+s, p2.y))) -
                    (L(tile, Point(p1.x, p1.y-s), Point(p2.x-s, p2.y)) *
                        meanIntensityStLine(tile, Point(p1.x, p1.y-s), Point(p2.x-s, p2.y)));
            sum2 += L(tile, Point(p1.x, p1.y+s), Point(p2.x+s, p2.y)) -
                    L(tile, Point(p1.x, p1.y-s), Point(p2.x-s, p2.y));
        }
    }
    return fabs(sum1/sum2);
}

// This will have to be in a loop for the upper level tile
double meanIntensityCurve(double L1, double F1, double L2, double F2) {
    return ((L1*F1 + L2*F2)/(L1+L2));
}

double meanIntensityStLine(Mat& tile, Point p1, Point p2) {
    return integrate(tile, p1, p2)/L(tile, p1, p2);
}

double L(Mat& tile, Point p1, Point p2) {
    return 0.0;
}

double integrate(Mat& tile, Point p1, Point p2) {

    int incr, totalPix;
    double intensity=0;

    if (p2.y > p1.y) yincr = 1;
    else yincr = -1;
    if (p2.x > p1.x) xincr = 1;
    else xincr = -1;
    if (abs(p2.y-p1.y) > abs(p2.x-p1.x)) {
        x = p2.x;
        yPerx = round(abs(p2.y-p1.y)/abs(p2.x-p1.x));
        int count = 0;
        for (int y=p1.y; y!=p2.y; y+=yincr) {
            intensity += imagePixelValue at (x,y);
            count++;
            if (count == yPerx) {
                x = x+xincr;
                count = 0;
            }
            totalPix++;
        }
    }
    else {
        y = p2.y;
        xPery = round(abs(p2.x-p1.x)/abs(p2.y-p1.y));
        int count = 0;
        for (int x=p1.x; x!=p2.x; x+=xincr) {
            intensity += imagePixelValue at (x,y);
            count++;
            if (count == xPery) {
                y = y+yincr;
                count = 0;
            }
            totalPix++;
        }
    }

    return intensity/totalPix;
}

